<?php
return array(
	'viewPath'=>APP_DIR . "/views/",
	'basePath'=>APP_DIR . '/protected/',//protected根目录
	'name'=>'ps',//应用名
	'runtimePath'=>APP_DIR . "/var/runtime",//运行时目录，主要用于模板的编译
	//预先import的命名空间
	'import'=>array(
		'application.lib.models.*',
		'application.lib.services.*',
		'application.lib.classes.*',
	),
	//模块配置，各部分的默认值为：module=default,controller=index,action=index
	'modules'=>array(
		'default',//这是默认加载的模块
		'admin',//admin模块
	),
	//组建配置
	'components'=>array(
		//模板渲染组件，这里统一采用smarty引擎
		'viewRenderer'=>array(
		  'class'=>'ExSmartyView',//支持smarty引擎的插件
		  'fileExtension' => '.tpl',//模板后缀名
		  /*
		   * 这里可用来配置全局变量，例如下面的配置，我们在模板种可以直接用<{CONST.cssRoot}>来读取
		   */
		  'globalVal' => array(
			  'cssRoot' =>"http://www.domain.com/css/",
		  ),
		  //这里为Smarty支持的属性
		  'config' => array(
		  	'left_delimiter' => "<{",
			'right_delimiter' => "}>",
		  	'template_dir' => APP_DIR . '/tmp/',
		  )
		),
		//URLRewrite组件，根据需要进行配置
		'urlManager'=>array(
			'urlFormat'=>'path',
			'rules'=>array(
				'<module:\w+>/<controller:\w+>/<action:\w+>'=>'<module>/<controller>/<action>',
                '<controller:\w+>/<action:\w+>'=>'default/<controller>/<action>',
				'<action:\w+>'=>'default/index/<action>',
				''=>'default/index/index',
			),
		), 
		//数据库组件
		'db'=>array(
			'class' => 'CDbConnection',
			'connectionString' => 'mysql:host=127.0.0.1;dbname=lianjia',
			'emulatePrepare' => true,
			'username' => 'root',
			'password' => '111111',
			'charset' => 'utf8',
		),
        //正常的log组件
		'log'=>array(
			'class'=>'CLogRouter',
			'routes'=>array(
				array(
					'class'=>'ExFileLogRoute',//支持按日期分割的日志类
					'levels'=>'error, warning,info,trace',
					'logPath'=> APP_DIR . '/var/logs/{Ymd}/'//支持日期格式,{}中的为日期格式
				), 
				array(
					'class'=>'CWebLogRoute',//仅在调试时打开
				), 
			),
		),
	),

	'preload'=>array('log'),//预先加载log组建
);

ini_set("display_errors", "On");
error_reporting(E_ALL | E_STRICT);
