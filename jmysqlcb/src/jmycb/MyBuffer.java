package jmycb;

public class MyBuffer {
	static int INIT_BUF_SIZE = 10240;
	byte[] buf;

	int pos;
	int catacity;
	int limit;

	MyPacker packer;

	public MyBuffer() {
		packer = new MyPacker(false);

		buf = new byte[INIT_BUF_SIZE];
		pos = 0;
		limit = 0;
		catacity = INIT_BUF_SIZE;
	}

	public void reset() {
		pos = 0;
		limit = 0;
	}

	public void setPos(int pos) {
		this.pos = pos;
	}

	public void setLimit(int limit) {
		this.limit = limit;
	}

	public int remain() {
		return limit - pos;
	}

	public byte[] readBytes() {
		byte[] bytes = new byte[limit];
		System.arraycopy(buf, 0, bytes, 0, limit);
		pos = limit;
		return bytes;
	}

	public void setBuf(byte[] bytes) {
		reset();
		System.arraycopy(bytes, 0, buf, 0, bytes.length);
		limit = bytes.length;
	}

	public void writeNum(long num, int len) {
		byte[] bytes = packer.pack(num, len);
		writeBytes(bytes);
	}

	public void writeUInt8(int num) {
		writeNum(num, 1);
	}

	public void writeUInt16(int num) {
		writeNum(num, 2);
	}

	public void writeUInt24(int num) {
		writeNum(num, 3);
	}

	public void writeUInt32(long num) {
		writeNum(num, 4);
	}

	public void writeUInt64(long num) {
		writeNum(num, 8);
	}

	public void writeBytes(byte[] bytes) {
		System.arraycopy(bytes, 0, buf, pos, bytes.length);
		pos += bytes.length;
	}
 

	public void writeNullString(String str) {
		byte[] bytes = str.getBytes();
		writeBytes(bytes);
		writeUInt8(0);
	}

	public long readNum(int len) {
		long num = packer.unpack(readBytes(len), len);
		return num;
	}

	public int readUInt8() {
		return (int) readNum(1);
	}

	public int readUInt16() {
		return (int) readNum(2);
	}

	public int readUInt24() {
		return (int) readNum(3);
	}

	public long readUInt32() {
		return readNum(4);
	}

	public long readUInt64() {
		return readNum(8);
	}

	public String readNullString() {
		int start = pos;
		while (buf[pos] != 0) {
			pos++;
		}
		pos++;
		return new String(buf, start, pos - start);
	}

	public String readFixedString(int len) {
		String s = new String(buf, pos, len);
		pos += len;
		return s;
	}

	public byte[] readBytes(int len) {
		byte[] strBytes = new byte[len];
		System.arraycopy(buf, pos, strBytes, 0, len);
		pos += len;
		return strBytes;
	}
}
