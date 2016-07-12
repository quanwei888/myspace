<?php
class EchoService {
		public function getText() {
			$testClass = new TestClass();
			return $testClass->helloWorld();
		}
}
