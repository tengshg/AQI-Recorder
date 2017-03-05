def pipeSource(func, targets):
    try:
        while True:
            item = func()
            if item:
                for target in targets:
                    target.send(item)
    except KeyboardInterrupt:
        for target in targets:
            target.close()

def pipeMiddle(func, targets):
    def theCoroutine(targets):
        try:
            while True:
                # Get item
                item = (yield)
                # Transfor item
                item = func(item)
                # Send it along to the next stage
                if item:
                    for target in targets:
                        target.send(item)
        except GeneratorExit:
            for target in targets:
                target.close()

    cor = theCoroutine(targets)
    cor.send(None)
    return cor

def pipeSink(func):
    def theCoroutine():
        try:
            while True:
                # Get item
                item = (yield)
                # Transfor item
                func(item)
        except GeneratorExit:
            pass

    cor = theCoroutine()
    cor.send(None)
    return cor


if __name__ == '__main__':
    pipeSource(lambda:"test", [pipeMiddle(lambda x: x + " OK", [pipeSink(print)])])
