package jmycb;

/**
 * java版二进制打包类
 * @author quanwei
 *
 */
public class MyPacker {
	boolean bigEndian = true;

	public MyPacker() {
	}

	public MyPacker(boolean bigEndian) {
		this.bigEndian = bigEndian;
	}

	public byte[] packInt16(short num) {
		return pack(num, 2);
	}

	public byte[] packUInt16(int num) {
		return pack(num, 2);
	}

	public byte[] packInt32(int num) {
		return pack(num, 4);
	}

	public byte[] packUInt32(long num) {
		return pack(num, 4);
	}

	public byte[] packInt64(long num) {
		return pack(num, 8);
	}

	byte[] pack(long num, int len) {
		byte[] stream = new byte[len];

		int maskOffset = (len - 1) * 8;
		byte first = (byte) ((num >> maskOffset & 0xff) | (num >>> 56 & 0x80));
		if (bigEndian) {
			stream[0] = first;
		} else {
			stream[len - 1] = first;
		}

		for (int i = 1; i < len; i++) {
			int offset = (len - i - 1) * 8;
			byte tmp = (byte) (num >> offset & 0xff);
			if (bigEndian) {
				stream[i] = tmp;
			} else {
				stream[len - i - 1] = tmp;
			}
		}

		return stream;

	}

	public short unpackInt16(byte[] stream) {
		return (short) unpack(stream, 2);
	}

	public int unpackUInt16(byte[] stream) {
		return (int) unpack(stream, 2);
	}

	public int unpackInt32(byte[] stream) {
		return (int) unpack(stream, 4);
	}

	public long unpackUInt32(byte[] stream) {
		return unpack(stream, 4);
	}

	public long unpackInt64(byte[] stream) {
		return unpack(stream, 8);
	}

	long unpack(byte[] stream, int len) {
		long num = 0;
		if (bigEndian) {
			for (int i = 0; i < len; i++) {
				num = (num << 8) | (stream[i] & 0xff);
			}
		} else {
			for (int i = len - 1; i >= 0; i--) {
				num = (num << 8) | (stream[i] & 0xff);
			}
		}
		return num;
	}
}
