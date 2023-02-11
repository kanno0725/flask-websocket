import psutil

def get_mem_rate():
    mem = psutil.virtual_memory()
    return mem.percent

if __name__ == "__main__":
    print(get_mem_rate())
