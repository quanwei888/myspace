<?php
class IndexController extends CController {
    public function actionIndex() {
		$echoService = new EchoService();
		$text = $echoService->getText();
        $model = UserModel::model();
        $this->render ( "index" ,array('text'=>$text));
    }
    public function actionDb() {
        echo 111;
    }
}
