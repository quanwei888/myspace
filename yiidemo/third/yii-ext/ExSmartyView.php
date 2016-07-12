<?php
/**
 * smarty支持
 * 
 * @author quanwei
 *
 */
class ExSmartyView extends CApplicationComponent implements IViewRenderer {
	public $globalVal = array ();
	/**
	 *
	 * @var string the file-extension for viewFiles this renderer should handle
	 *      for smarty templates this usually is .tpl
	 */
	public $fileExtension = '.tpl';
	
	/**
	 *
	 * @var int dir permissions for smarty compiled templates directory
	 */
	public $directoryPermission = 0771;
	
	/**
	 *
	 * @var int file permissions for smarty compiled template files
	 *      NOTE: BEHAVIOR CHANGED AFTER VERSION 0.9.8
	 */
	public $filePermission = 0644;
	
	/**
	 *
	 * @var null string alias of the directory where your smarty plugins are
	 *      located
	 *      application.extensions.Smarty.plugins is always added
	 */
	public $pluginsDir = null;
	
	/**
	 *
	 * @var null string alias of the directory where your smarty
	 *      template-configs are located
	 */
	public $configDir = null;
	protected static $baseUrl;
	
	/**
	 *
	 * @var array smarty configuration values
	 *      this array is used to configure smarty at initialization you can set
	 *      all
	 *      public properties of the Smarty class e.g. error_reporting
	 *     
	 *      please note:
	 *      compile_dir will be created if it does not exist, default is
	 *      <app-runtime-path>/smarty/compiled/
	 *     
	 * @since 0.9.9
	 */
	public $config = array ();
	
	/**
	 *
	 * @var Smarty smarty instance for rendering
	 */
	private $smarty = null;
	
	/**
	 * smarty注册函数
	 *
	 * @var array
	 */
	public $modifiers = array ();
	
	/**
	 * Component initialization
	 */
	public function init() {
		
		parent::init ();
		
		Yii::import ( 'application.vendors.*' );
		
		// need this to avoid Smarty rely on spl autoload function,
		// this has to be done since we need the Yii autoload handler
		if (! defined ( 'SMARTY_SPL_AUTOLOAD' )) {
			define ( 'SMARTY_SPL_AUTOLOAD', 0 );
		} elseif (SMARTY_SPL_AUTOLOAD !== 0) {
			throw new CException ( 'ESmartyViewRenderer cannot work with SMARTY_SPL_AUTOLOAD enabled. Set SMARTY_SPL_AUTOLOAD to 0.' );
		}
		
		// including Smarty class and registering autoload handler
		require_once ('Smarty/sysplugins/smarty_internal_data.php');
		require_once ('Smarty/Smarty.class.php');
		
		// need this since Yii autoload handler raises an error if class is not
		// found
		// Yii autoloader needs to be the last in the autoload chain
		spl_autoload_unregister ( 'smartyAutoload' );
		Yii::registerAutoloader ( 'smartyAutoload' );
		
		$this->smarty = new Smarty ();
		
		// configure smarty
		if (is_array ( $this->config )) {
			foreach ( $this->config as $key => $value ) {
				if ($key {0} != '_') { // not setting semi-private properties
					$this->smarty->$key = $value;
				}
			}
		}
		$this->smarty->_file_perms = $this->filePermission;
		$this->smarty->_dir_perms = $this->directoryPermission;
		
		if (! $this->smarty->template_dir) {
			$this->smarty->template_dir = '';
		}
		$compileDir = isset ( $this->config ['compile_dir'] ) ? $this->config ['compile_dir'] : Yii::app ()->getRuntimePath () . '/smarty/compiled/';
		
		// create compiled directory if not exists
		if (! file_exists ( $compileDir )) {
			mkdir ( $compileDir, $this->directoryPermission, true );
		}
		$this->smarty->compile_dir = $compileDir; // no check for trailing /,
		                                          // smarty does this for us
		
		if (! empty ( $this->configDir )) {
			$this->smarty->config_dir = Yii::getPathOfAlias ( $this->configDir );
		}
		
		$this->smarty->registerPlugin ( "block", "action", array (
			&$this, 
			"block" 
		) );
		foreach ( $this->modifiers as $name => $modifier ) {
			$this->smarty->registerPlugin ( "modifier", $name, $modifier );
		}
	}
	
	public function getBaseUrl() {
		if (self::$baseUrl === null) {
			self::$baseUrl = Yii::app ()->getRequest ()->getBaseUrl ();
		}
		return self::$baseUrl;
	}
	
	/**
	 * Renders a view file.
	 * This method is required by {@link IViewRenderer}.
	 *
	 * @param
	 *       	 CBaseController the controller or widget who is rendering the
	 *       	 view file.
	 * @param
	 *       	 string the view file path
	 * @param
	 *       	 mixed the data to be passed to the view
	 * @param
	 *       	 boolean whether the rendering result should be returned
	 * @return mixed the rendering result, or null if the rendering result is
	 *         not needed.
	 */
	public function renderFile($context, $sourceFile, $data, $return) {
		// current controller properties will be accessible as {$this.property}
		$data ['this'] = $context;
		// Yii::app()->... is available as {Yii->...} (deprecated, use
		// {Yii::app()->...} instead, Smarty3 supports this.)
		$data ['Yii'] = Yii::app ();
		// time and memory information
		$data ['TIME'] = sprintf ( '%0.5f', Yii::getLogger ()->getExecutionTime () );
		$data ['MEMORY'] = round ( Yii::getLogger ()->getMemoryUsage () / (1024 * 1024), 2 ) . ' MB';
		$data ['BASE_URL'] = $this->getBaseUrl ();
		$data ['_GET'] = $_GET;
		$data ['_POST'] = $_POST;
		
		foreach ( $this->globalVal as $key => $val ) {
			$data ['CONST'] [$key] = $val;
		}
		// check if view file exists
		if (! is_file ( $sourceFile ) || ($file = realpath ( $sourceFile )) === false) {
			throw new CException ( Yii::t ( 'yiiext', 'View file "{file}" does not exist.', array (
				'{file}' => $sourceFile 
			) ) );
		}
		
		// changed by simeng in order to use smarty debug
		foreach ( $data as $key => $value ) {
			$this->smarty->assign ( $key, $value );
		}
		
		// render or return
		if ($return) {
			ob_start ();
		}
		$this->smarty->display ( $sourceFile );
		if ($return) {
			$res = ob_get_contents ();
			ob_end_clean ();
			return $res;
		}
	}
	
	function block($params, $content, $smarty, &$repeat, $template = 1) {
		$repeat = false;
		$m = isset ( $params ['module'] ) ? $params ['module'] : "default";
		$c = isset ( $params ['controller'] ) ? $params ['controller'] : "index";
		$a = isset ( $params ['action'] ) ? $params ['action'] : "index";
		
		if (isset($params ['module'])) {
			unset($params ['module']);
		}
		if (isset($params ['controller'])) {
			unset($params ['controller']);
		}
		if (isset($params ['action'])) {
			unset($params ['action']);
		}
		
		foreach ($params as $key=>$val) {
			if (!isset($_GET[$key])) {
				$_GET[$key] = $val;
			}
		}
		
		ob_start ();
		Yii::app ()->runController ( "$m/$c/$a" );
		$content = ob_get_clean ();
		return $content;
	}
}
