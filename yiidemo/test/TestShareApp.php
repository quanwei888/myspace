<?php
/**
 * test case.
 */
class TestShareApp extends PHPUnit_Framework_TestCase {
    /**
     * 
     * Enter description here ...
     * @var ShareApp
     */
    public $shareApp;
    public function setUp() {
        $this->shareApp = new ShareApp ();
        $this->shareApp->apps = array (
                'a' => array (
                        'url' => 'http://www.a.com/', 
                        'name' => 'aaa', 
                        'attr' => array (
                                'url' => 'url1', 
                                'title' => 'title1', 
                                'summary' => 'summary1', 
                                'desc' => 'desc1', 
                                'pic' => 'pic1', 
                                'src' => 'src1' 
                        ), 
                        'const' => array (
                                'appkey' => "123456" 
                        ) 
                ), 
                'b' => array (
                        'url' => 'http://www.b.com/', 
                        'name' => 'bbb', 
                        'attr' => array (
                                'url' => 'url1', 
                                'title' => false, 
                                'summary' => 'summary1', 
                                'desc' => 'desc1', 
                                'pic' => 'pic1', 
                                'src' => 'src1' 
                        ), 
                        'const' => array (
                                'appkey' => "123456" 
                        ) 
                ) 
        );
    }
    
    public function testGetRedirectUrl() {
        $info = array ();
        $info ['url'] = "http://www.jike.com";
        $info ['title'] = "中国";
        $info ['summary'] = "$%^&*()_";
        $info ['desc'] = "中国中国!@#$%^&*()!@#$%中国中国中";
        $info ['pic'] = "http://www.jike.com/a.jpg";
        $info ['src'] = "即刻搜索";
        
        $url = $this->shareApp->getRedirectUrl ( "a", $info );
        $expected = "http://www.a.com/?";
        $expected .= "appkey=123456&";
        $expected .= "url1=" . urlencode ( $info ['url'] ) . "&";
        $expected .= "title1=" . urlencode ( $info ['title'] ) . "&";
        $expected .= "summary1=" . urlencode ( $info ['summary'] ) . "&";
        $expected .= "desc1=" . urlencode ( $info ['desc'] ) . "&";
        $expected .= "pic1=" . urlencode ( $info ['pic'] ) . "&";
        $expected .= "src1=" . urlencode ( $info ['src'] );
        $this->assertEquals ( $expected, $url );
        
        $url = $this->shareApp->getRedirectUrl ( "b", $info );
        $expected = "http://www.b.com/?";
        $expected .= "appkey=123456&";
        $expected .= "url1=" . urlencode ( $info ['url'] ) . "&";
        $expected .= "summary1=" . urlencode ( $info ['summary'] ) . "&";
        $expected .= "desc1=" . urlencode ( $info ['desc'] ) . "&";
        $expected .= "pic1=" . urlencode ( $info ['pic'] ) . "&";
        $expected .= "src1=" . urlencode ( $info ['src'] );
        $this->assertEquals ( $expected, $url );
    }

}

