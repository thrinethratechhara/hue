/*
 * Licensed to Cloudera, Inc. under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  Cloudera, Inc. licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package com.cloudera.hue.livy.server

import com.cloudera.hue.livy.LivyConf
import com.cloudera.hue.livy.server.sessions.ProcessSession
import com.cloudera.hue.livy.sessions.Spark
import org.scalatest.{BeforeAndAfter, FunSpecLike, Matchers}

class ProcessSessionSpec extends BaseSessionSpec with FunSpecLike with Matchers with BeforeAndAfter {

  val livyConf = new LivyConf()
  livyConf.set("livy.repl.driverClassPath", sys.props("java.class.path"))

  def createSession() = ProcessSession.create(livyConf, 0, Spark())
}
