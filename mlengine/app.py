from pyspark import SparkConf, SparkContext
from flask import Flask, jsonify, request

conf = SparkConf()
conf.setMaster("local")
conf.setAppName("SparkContext1")
conf.set("spark.executor.memory", "1g")

app = Flask(__name__)


if __name__ == '__main__':
    app.run()
