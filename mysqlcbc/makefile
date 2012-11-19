VERSION = mysqlcb-1.0

MYSQL_LIB=/usr/lib/
MYSQL_INCLUDE=/usr/include/mysql/
 

INCLUDES=-I. \
	 -I$(MYSQL_INCLUDE)
		
LDFLAGS=-L$(MYSQL_LIB) -lmysqlclient \
	-lpthread -lrt

CC=g++
ifeq ($(MODE),C++)
	CXXFLAGS=-g -finline-functions -Wall -Winline -pipe -D__VERSION_ID__="\"$(VERSION_ID)\"" $(VERSION_SIGN) -DDEBUG
else
	CXXFLAGS=-g -finline-functions -Wall -Winline -pipe -D__VERSION_ID__="\"$(VERSION_ID)\"" $(VERSION_SIGN) -DDEBUG -D_cplusplus
endif
TARGET=mysqlcb
LIBTARGET=libmysqlcb.so
OBJECTS=test.o mysqlcb.o mysqlcb_buffer.o

all:$(TARGET)
$(TARGET):$(OBJECTS)
	$(CC) -o $@ $(OBJECTS) $(LDFLAGS)   
	$(CC) -o lib$@.so $(OBJECTS) $(LDFLAGS) -fPIC -shared
%.o : %.c
	$(CC) $(CXXFLAGS) -c $< -o $@ $(INCLUDES) -fPIC -shared
clean:
	rm -f *.o $(TARGET) $(LIBTARGET)
