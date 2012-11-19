package jmycb;

import java.io.IOException;

public class MyTest {

	/**
	 * @param args
	 * @throws IOException
	 */
	public static void main(String[] args) throws Exception {
		MySlave slave = new MySlave("127.0.0.1", 3306, "root", "1111111", 10000,
				"/tmp/ralay");
		slave.connect();
	}

}
