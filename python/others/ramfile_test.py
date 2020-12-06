from memory_tempfile import MemoryTempfile

def main():
    tempfile = MemoryTempfile()
    with tempfile.TemporaryFile() as tf:
        tf.write(b'It works !!')
        tf.seek(0)
        print(tf.read())

if __name__ == '__main__':
    main()
