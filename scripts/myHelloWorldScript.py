import sys

# python ./scripts/MyHelloWorld.py Paulo

def myHelloWorldScript(myName: str):
    print ("Hello " + myName + "!")


if __name__ == "__main__":
    myName = str(sys.argv[1])
    myHelloWorldScript(myName)

# Curiosos sobre este último bloco de código?
# Explicação: https://realpython.com/if-name-main-python/