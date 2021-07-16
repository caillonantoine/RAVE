import torch
from torch.utils.data import DataLoader, random_split
from fd.parallel_model.model import ParallelModel
from udls import SimpleDataset, simple_audio_preprocess
from effortless_config import Config
import pytorch_lightning as pl
from os import environ

if __name__ == "__main__":

    class args(Config):
        DATA_SIZE = 1
        CAPACITY = 64
        LATENT_SIZE = 16
        RATIOS = [8, 8, 4, 4]
        BIAS = True
        STUDENT_CHKPT = None
        D_CAPACITY = 16
        D_MULTIPLIER = 4
        D_N_LAYERS = 4
        WARMUP = 100000

        PREPROCESSED = None
        WAV = None
        SR = 24000
        N_SIGNAL = 16384

        BATCH = 8
        CUDA = 0

    args.parse_args()

    environ["CUDA_VISIBLE_DEVICES"] = str(args.CUDA)

    model = ParallelModel(
        data_size=args.DATA_SIZE,
        capacity=args.CAPACITY,
        latent_size=args.LATENT_SIZE,
        ratios=args.RATIOS,
        bias=args.BIAS,
        d_capacity=args.D_CAPACITY,
        d_multiplier=args.D_MULTIPLIER,
        d_n_layers=args.D_N_LAYERS,
        warmup=args.WARMUP,
        sr=args.SR,
    )

    dataset = SimpleDataset(
        args.PREPROCESSED,
        args.WAV,
        preprocess_function=simple_audio_preprocess(args.SR, args.N_SIGNAL),
        split_set="full",
    )

    val = (2 * len(dataset)) // 100
    train = len(dataset) - val
    train, val = random_split(dataset, [train, val])

    train = DataLoader(train, args.BATCH, True, drop_last=True)
    val = DataLoader(val, args.BATCH, False)

    trainer = pl.Trainer(
        gpus=1,
        val_check_interval=0.1,
    )
    trainer.fit(model, train, val)