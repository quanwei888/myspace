package jmycb;

import java.security.*;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.SelectionKey;
import java.nio.channels.Selector;
import java.nio.channels.SocketChannel;
import java.util.Iterator;

public class MySlave {
	static int CLIENT_PLUGIN_AUTH = 0x00080000;
	static int CLIENT_PROTOCOL_41 = 0x00000200;
	static int CLIENT_PLUGIN_AUTH_LENENC_CLIENT_DATA = 0x00200000;
	static int CLIENT_SECURE_CONNECTION = 0x00008000;
	static int CLIENT_CONNECT_WITH_DB = 0x00000008;
	static int CLIENT_CONNECT_ATTRS = 0x00100000;

	String host;
	int port;
	String userName;
	String password;
	int serverId;
	String ralayPath;

	SocketChannel socket;
	Selector selector;
	SelectionKey socketKey;

	MyBuffer readBuf;
	MyBuffer writeBuf;

	int connTimeout = 3000;
	int readTimeout = 3000;
	int writeTimeout = 3000;

	String authName;
	String seed;
	byte[] authData;
	int capabilities;
	int charset;
	long connId;
	String version;
	int errno;
	String error;

	public MySlave(String host, int port, String userName, String password,
			int serverId, String ralayPath) {
		super();
		this.host = host;
		this.port = port;
		this.userName = userName;
		this.password = password;
		this.serverId = serverId;
		this.ralayPath = ralayPath;

		readBuf = new MyBuffer();
		writeBuf = new MyBuffer();

	}

	public void connect() throws Exception {
		socket = SocketChannel.open();
		socket.configureBlocking(false);

		selector = Selector.open();

		socket.register(selector, SelectionKey.OP_CONNECT);
		socket.connect(new InetSocketAddress(host, port));
		if (selector.select(connTimeout) == 0) {
			// 连接超时
			throw new Exception("connect master server timeout");
		}

		// 取消事件
		Iterator<SelectionKey> keyIter = selector.selectedKeys().iterator();
		socketKey = keyIter.next();
		keyIter.remove();
		if (!socket.finishConnect()) {
			throw new Exception("connect master server fail");
		}

		// 连接成功
		login();
	}

	public void login() throws Exception {
		readPackat();
		parseInitPacket();
		buildAuthPacket();
		writePacket();
		readPackat();
		parseResultPacket();

	}

	public void sendDumpCmd() {

	}

	public void flushLog() {

	}

	public void writePacket() throws Exception {
		socketKey.interestOps(SelectionKey.OP_WRITE);
		ByteBuffer buf = ByteBuffer.allocate(writeBuf.limit);
		buf.put(writeBuf.readBytes());
		buf.flip();
		write(buf, writeTimeout);
	}

	public void readPackat() throws Exception {
		socketKey.interestOps(SelectionKey.OP_READ);
		readBuf.setBuf(read(4, readTimeout));
		int bodyLen = readBuf.readUInt24();
		readBuf.readUInt8();// sid

		readBuf.setBuf(read(bodyLen, readTimeout));
	}

	public void buildAuthPacket() throws Exception {
		writeBuf.reset();
		writeBuf.setPos(4);
		writeBuf.writeUInt32(capabilities);
		writeBuf.writeUInt32(0x1000000);
		writeBuf.writeUInt8(charset);
		writeBuf.writeBytes(new byte[23]);
		writeBuf.writeNullString(userName);
		
		byte[] authResponst = scramble411(password, seed);
		if ((capabilities & CLIENT_PLUGIN_AUTH_LENENC_CLIENT_DATA) > 0) {
			writeBuf.writeUInt8(authResponst.length);
		} else if ((capabilities & CLIENT_SECURE_CONNECTION) > 0) {
			writeBuf.writeUInt8(authResponst.length);
		}
		writeBuf.writeBytes(authResponst);

		if ((capabilities & CLIENT_CONNECT_WITH_DB) > 0) {
			writeBuf.writeNullString("test");
		}
		if ((capabilities & CLIENT_PLUGIN_AUTH) > 0) {
			writeBuf.writeBytes(authName.getBytes());
		}
		writeBuf.setLimit(writeBuf.pos);
		writeBuf.setPos(0);
		writeBuf.writeUInt24(writeBuf.limit - 4);
		writeBuf.writeUInt8(1);

	}

	public void buildDumpCmdPacket() {

		writeBuf.reset();
		writeBuf.setPos(4);
		
		writeBuf.writeUInt8(0x12);
		
		
		writeBuf.setLimit(writeBuf.pos);
		writeBuf.setPos(0);
		writeBuf.writeUInt24(writeBuf.limit - 4);
		writeBuf.writeUInt8(1);
	}
	public void parseResultPacket() throws Exception {
		int type = readBuf.readUInt8();
		if (type == 0xff) {
			errno = readBuf.readUInt16();
			if ((capabilities & CLIENT_PROTOCOL_41) > 0) {
				error = "[" + readBuf.readFixedString(6) +"]";
			}
			error += readBuf.readFixedString(readBuf.remain());
			throw new Exception(error);
		} else if (type == 0x00) {

		}

	}

	public void parseInitPacket() throws Exception {
		readBuf.readUInt8();// protocolVersion
		version = readBuf.readNullString();
		/*
		 * String version = versionDesc.substring(0, versionDesc.indexOf("-") -
		 * 1); String[] cols = version.split("\\."); int versionNum =
		 * Integer.parseInt(cols[0]) * 10000 + Integer.parseInt(cols[1]) * 100 +
		 * Integer.parseInt(cols[2]);
		 */
		connId = readBuf.readUInt32();
		byte[] authData1 = readBuf.readBytes(8);
		readBuf.readUInt8();
		int capabilities1 = readBuf.readUInt16();
		if (readBuf.remain() == 0) {
			return;
		}
		charset = readBuf.readUInt8();
		readBuf.readUInt16();// statusFlag
		int capabilities2 = readBuf.readUInt16();

		capabilities = ((int) capabilities2 << 16) | (int) capabilities1;

		int len = 0;
		if ((capabilities & CLIENT_PLUGIN_AUTH) > 0) {
			len = readBuf.readUInt8();
		} else {
			readBuf.readUInt8();
		}
		readBuf.readBytes(10);// reserved
		byte[] authData2 = new byte[0];
		if ((capabilities & CLIENT_SECURE_CONNECTION) > 0) {
			authData2 = new byte[len - 8];
			authData2 = readBuf.readBytes(len - 8);
			if ((capabilities & CLIENT_PLUGIN_AUTH) > 0) {
				authName = readBuf.readFixedString(readBuf.remain());
			}
		}
		authData = new byte[authData1.length + authData2.length];
		System.arraycopy(authData1, 0, authData, 0, authData1.length);
		System.arraycopy(authData2, 0, authData, authData1.length,
				authData2.length);
		seed = new String(authData, 0, authData.length - 1);

	}

	public byte[] read(int len, int timeout) throws Exception {
		ByteBuffer buf = ByteBuffer.allocate(len);
		buf.position(0);
		buf.limit(len);

		int newTimeout = timeout;
		while (buf.remaining() > 0 && (timeout == 0 || newTimeout > 0)) {
			if (selector.select(newTimeout) == 0) {
				throw new Exception("read packet from master server timeout");
			}
			Iterator<SelectionKey> keyIter = selector.selectedKeys().iterator();
			keyIter.next();
			keyIter.remove();

			int nbytes = socket.read(buf);
			if (nbytes <= 0 && buf.remaining() > 0) {
				throw new Exception("read error");
			}
		}

		if (buf.remaining() > 0) {
			throw new Exception("read timeout");
		}

		buf.flip();

		byte[] tmpBytes = new byte[buf.limit()];
		buf.get(tmpBytes);

		return tmpBytes;
	}

	public void write(ByteBuffer buf, int timeout) throws Exception {
		int newTimeout = timeout;
		while (buf.remaining() > 0 && (timeout == 0 || newTimeout > 0)) {
			if (selector.select(newTimeout) == 0) {
				throw new Exception("write packet from master server timeout");
			}

			Iterator<SelectionKey> keyIter = selector.selectedKeys().iterator();
			keyIter.next();
			keyIter.remove();

			int nbytes = socket.write(buf);
			if (nbytes <= 0 && buf.remaining() > 0) {
				throw new Exception("read error");
			}
		}

		if (buf.remaining() > 0) {
			throw new Exception("read timeout");
		}
	}

	public void start() {

	}

	public void stop() {

	}

	static byte[] scramble411(String password, String seed)
			throws NoSuchAlgorithmException {
		MessageDigest md = MessageDigest.getInstance("SHA-1"); //$NON-NLS-1$

		byte[] passwordHashStage1 = md.digest(password.getBytes());
		md.reset();

		byte[] passwordHashStage2 = md.digest(passwordHashStage1);
		md.reset();

		byte[] seedAsBytes = seed.getBytes(); // for debugging
		md.update(seedAsBytes);
		md.update(passwordHashStage2);

		byte[] toBeXord = md.digest();

		int numToXor = toBeXord.length;

		for (int i = 0; i < numToXor; i++) {
			toBeXord[i] = (byte) (toBeXord[i] ^ passwordHashStage1[i]);
		}

		return toBeXord;
	}
}
