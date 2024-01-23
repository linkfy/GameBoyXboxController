rm main.gb
rgbasm -L -o main.o main.asm
rgblink -o main.gb main.o
rgbfix -v -p 0xFF main.gb