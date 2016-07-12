<?php
define ( "APP_DIR", dirname ( dirname ( __FILE__ ) ) );
defined ( 'YII_DEBUG' ) or define ( 'YII_DEBUG', true );
defined ( 'YII_TRACE_LEVEL' ) or define ( 'YII_TRACE_LEVEL', 3 );

require_once (APP_DIR . '/third/yii/framework/yii.php');
Yii::setPathOfAlias ( 'third', APP_DIR . "/third" ); //third namespace
Yii::import ( "third.yii-ext.*" ); //import yiiext
Yii::import ( "third.*" ); //import third 

//run app
Yii::createWebApplication ( APP_DIR . "/protected/config/main.php" )->run ();
