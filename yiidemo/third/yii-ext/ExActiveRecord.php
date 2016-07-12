<?php
/**
 * 封装了CActiveRecord，用于应用model继承
 * 
 * @author quanwei
 *
 */
abstract class ExActiveRecord extends CActiveRecord {
    /**
     * 一组自动添加字段名
     */
    public $addTimeField = 'addTime'; // 记录添加时间
    public $modTimeField = 'modTime'; // 记录修改时间
    public $addUserField = 'addUser'; // 记录添加人
    public $modUserField = 'modUser'; // 记录修改人

    /**
     * 数据库名
     *
     * @return string
     */
    public function databaseName() {
        return "";
    }

    /**
     * 数据库表名
     *
     * @see CActiveRecord::tableName()
     */
    public function tableName() {
        $table = get_class($this);
        $table = substr($table,0,strlen($table) - 5);
        if ($this->databaseName() == "") {
            return $table;
        } else {
            return $this->databaseName() . "." .$table;
        }
    }

    /**
     * 多数据库支持
     *
     * @see CActiveRecord::getDbConnection()
     */
    public function getDbConnection() {
        $db = Yii::app()->db;
        if ($db instanceof CDbConnection) {
            return $db;
        } else {
            throw new CDbException(Yii::t('yii','Active Record requires a "db" CDbConnection application component.'));
        }
    }

    /**
     * 获取model实例
     *
     * @return ZxActiveRecord
     */
    public static function model($class = "") {
        if ($class == "") {
            $class = get_called_class();
        }
        $model = parent::model($class);
        return $model;
    }

    public function beforeSave() {
        $addTime = time();
        $modTime = time();
        $addType = '';
        $modType = '';
        $metaData = $this->getMetaData();
        if (isset($metaData->columns [$this->addTimeField])) {
            $addType = $metaData->columns [$this->addTimeField]->dbType;
        }
        if (isset($metaData->columns [$this->modTimeField])) {
            $modType = $metaData->columns [$this->modTimeField]->dbType;
        }

        $currTime = date('Y-m-d H:i:s');
        if ($addType == "datetime") {
            $addTime = $currTime;
        }
        if ($modType == "datetime") {
            $modTime = $currTime;
        }
        
        // addTime && modTime
        if ($this->getIsNewRecord()) {
            if (isset($metaData->columns [$this->addTimeField]) && ! $this->getAttribute($this->addTimeField)) {
                $this->setAttribute($this->addTimeField,$addTime);
            }
        }
        
        if (isset($metaData->columns [$this->modTimeField])) {
            $this->setAttribute($this->modTimeField,$modTime);
        }
        
        return parent::beforeSave();
    }

    /**
     * 返回原始PDO对象
     * @return PDO
     */
    public function pdo() {
        $db = $this->getDbConnection();
        return $db->getPdoInstance();
    }
}
