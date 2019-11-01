import os
import sys

import torch
import torchvision

import advertorch
from advertorch.attacks.utils import multiple_mini_batch_attack


def get_benchmark_sys_info():
    rval = "#\n#\n"
    rval += ("# Automatically generated benchmark report "
             "(screen print of running this file)\n#\n")
    uname = os.uname()
    rval += "# sysname: {}\n".format(uname.sysname)
    rval += "# release: {}\n".format(uname.release)
    rval += "# version: {}\n".format(uname.version)
    rval += "# machine: {}\n".format(uname.machine)
    rval += "# python: {}.{}.{}\n".format(
        sys.version_info.major,
        sys.version_info.minor,
        sys.version_info.micro)
    rval += "# torch: {}\n".format(torch.__version__)
    rval += "# torchvision: {}\n".format(torchvision.__version__)
    rval += "# advertorch: {}\n".format(advertorch.__version__)
    return rval


def benchmark_robust_accuracy(
        model, loader, attack_class, attack_kwargs, device="cuda"):
    adversary = attack_class(model, **attack_kwargs)
    label, pred, advpred = multiple_mini_batch_attack(
        adversary, loader, device=device)
    accuracy = 100. * (label == pred).sum().item() / len(label)
    robust_accuracy = 100. * (label == advpred).sum().item() / len(label)

    rval = ""
    rval += "# attack type: {}\n".format(attack_class.__name__)

    prefix = " attack kwargs: "
    count = 0
    for key in attack_kwargs:
        this_prefix = prefix if count == 0 else " " * len(prefix)
        count += 1
        rval += "#{}{}={}\n".format(this_prefix, key, attack_kwargs[key])

    rval += "# data: {}\n".format(loader.name)
    rval += "# model: {}\n".format(model.name)
    rval += "# accuracy: {}%\n".format(accuracy)
    rval += "# robust accuracy: {}%\n".format(robust_accuracy)

    return rval
