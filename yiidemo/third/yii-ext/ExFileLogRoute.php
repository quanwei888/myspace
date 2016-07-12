<?php
/**
 * 支持日志切分的文件日志类
 * 
 * @author quanwei
 *
 */
class ExFileLogRoute extends CFileLogRoute {
	private static $requestId = "";
	public static function getRequestIdInt64() {
		$requestId = self::getRequestId ();
		return (hexdec ( substr ( $requestId, 0, 8 ) ) << 32) | hexdec ( substr ( $requestId, 0, - 8 ) );
	}
	public static function getRequestId() {
		if (self::$requestId == "") {
			self::$requestId = substr ( md5 ( microtime () . rand ( 1, 10000 ) ), 0, 16 );
		}
		return self::$requestId;
	}
	public function setLogPath($value) {
		$value = $this->getFormatPath ( $value );
		if (! file_exists ( $value )) {
			if (! @mkdir ( $value, 0775, true )) {
				if (! file_exists ( $value )) {
					throw new Exception ( "mkdir $value fail" );
				}
			}
		}
		return parent::setLogPath ( $value );
	}
	public function getFormatPath($value) {
		$callback = array (
			$this,
			"replace" 
		);
		$value = preg_replace_callback ( "/{[^}]*}/", $callback, $value );
		return $value;
	}
	protected function formatLogMessage($message, $level, $category, $time) {
		if('behavior' === $level){
			return"{$message}\n";
		}
		// show (us)
		$usecond = sprintf ( "%06d", $time / 1 * 1000000 % 1000000 );
		return @date ( '[Y/m/d H:i:s]', $time ) . " [$time] [" . self::getRequestId () . "] [$level] [$category] $message\n";
	}
	public function replace($matchs) {
		$format = date ( $matchs [0] );
		$format = str_replace ( "{", "", $format );
		$format = str_replace ( "}", "", $format );
		return $format;
	}
}
