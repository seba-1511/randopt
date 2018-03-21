#!/usr/bin/env python3

import randopt as ro

if __name__ == '__main__':
    exp = ro.Experiment('attach_example')
    attachment = {
        'bytes': bytes('hahahaha'.encode('utf-8')),
        'array': list(range(10)),
        'dict': dict(qwer=1, asdf=2),
        'int': 2,
        'float': 2.3,
    }
    exp.add_result(0, attachment=attachment)
    result = exp.minimum()
    print(result.attachment)
    assert attachment == result.attachment
