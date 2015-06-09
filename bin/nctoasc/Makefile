CFLAGS = -I/usr/include -I/usr/local/include -Wall -g

LFLAGS = -L/usr/lib -L/usr/local/lib

LIBS =   -lnetcdf -lz -lm -lc

CC   =  gcc

OBJECTS = nctoasc.o

nctoasc.exe:   $(OBJECTS)
	$(CC) -o $@ $(LFLAGS) $(OBJECTS) $(LIBS);


clean:	
	rm *.o *.bck
