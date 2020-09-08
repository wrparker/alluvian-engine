import copy


def copy_obj(objfrom, objto):
    for k, v in objfrom.__dict__.items():
        objto.__dict__[k] = copy.deepcopy(v)
