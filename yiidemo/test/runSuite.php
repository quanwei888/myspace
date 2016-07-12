<?php

define ( "APP_DIR", dirname ( dirname ( __FILE__ ) ) );
define ( "WWW_DIR", dirname ( APP_DIR ) );
defined ( 'YII_DEBUG' ) or define ( 'YII_DEBUG', true );
defined ( 'YII_TRACE_LEVEL' ) or define ( 'YII_TRACE_LEVEL', 3 );

require_once (WWW_DIR . '/thirdlib/yii/framework/yii.php');

Yii::setPathOfAlias ( 'jike', WWW_DIR . "/jikelib" ); //jike namespace
Yii::setPathOfAlias ( 'third', WWW_DIR . "/thirdlib" ); //third namespace
Yii::setPathOfAlias ( 'test', APP_DIR . "/test" ); //third namespace
Yii::import ( "jike.yiiext.*" ); //import jike.yiiext
Yii::import ( "third.*" ); //import third 
Yii::import ( "test.*" ); //import third 


Yii::createWebApplication ( APP_DIR . "/protected/config/main.php" );
require_once 'PHPUnit/Framework/TestCase.php';
require_once 'PHPUnit/Framework/TestSuite.php';

/**
 * Static test suite.
 */
class runSuite extends PHPUnit_Framework_TestSuite {
    
    /**
     * Constructs the test suite handler.
     */
    public function __construct() {
        $this->setName ( 'testSuite' );
        
        $this->addTestSuite ( 'TestShareApp' );
    
    }
    
    /**
     * Creates the suite.
     */
    public static function suite() {
        return new self ();
    }
}

