package jmycb;

import java.io.IOException;
import java.sql.*;
import java.sql.DriverManager;

public class MyTest1 {

	/**
	 * @param args
	 * @throws IOException
	 */
	public static void main(String[] args) throws Exception {
		Class.forName("com.mysql.jdbc.Driver");
		String url = "jdbc:mysql://127.0.0.1:3306/test?user=root&password=111111";
		Connection conn = DriverManager.getConnection(url);
		Statement stmt = conn.createStatement();
		String query = "select * from test";
		ResultSet rs = stmt.executeQuery(query);
		while (rs.next()) {
			rs.getString(1);
			rs.getInt(2);
			rs.getBigDecimal(1);
		}
		String upd = "insert into test (id,name) values(1001,xuzhaori)";
		int con = stmt.executeUpdate(upd);
	}

}
