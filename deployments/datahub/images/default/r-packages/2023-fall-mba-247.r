#!/usr/bin/env Rscript

source("/tmp/class-libs.R")

class_name = "MBA 247 Fall 2023"
class_libs = c(
  "caret", "6.0-94",
  "arules", "1.7-6",
  "arulesViz", "1.5-2",
  "h2o", "3.42.0.2",
  "tm", "0.7-11",
  "SnowballC", "0.7.1",
  "wordcloud", "2.6",
  "pROC", "1.18.4",
  "rpart.plot", "3.1.1",
  "randomForest","4.7-1.1",
  "xgboost","1.7.5.1"
)
class_libs_install_version(class_name, class_libs)
