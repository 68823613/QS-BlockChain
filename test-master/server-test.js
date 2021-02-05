// eslint-disabled
var express = require('express');
var compression = require('compression');
var fs = require('fs');
var open = require('opn');
var bodyParser = require('body-parser');
var multer = require('multer'); // v1.0.5
var upload = multer(); // for parsing multipart/form-data
var request = require('request');

function sendMsg(data) {
  typeof data == 'object' ?
  request.post(
    {
      url:'http://127.0.0.1:9999/api/postData',
      form: data,
      encoding:'utf8'
    },
    function(error, response, body){
      if(response.statusCode == 200){
          console.log(body);
      }else{
          console.log(response.statusCode);
      }
    }) :
    console.log('data-type err')
}

var app = express();

app.use(bodyParser.json()); // for parsing application/json
app.use(bodyParser.urlencoded({ extended: true }));

app.use(compression());

app.use('/', express.static(__dirname));

app.use(function(req, res, next) {
		res.header('Access-Control-Allow-Origin', '*');
    res.header("X-Powered-By",' 3.2.1');
		res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, x-token, Allow, authorization');
    res.header('Access-Control-Allow-Methods', 'PUT,POST,GET,DELETE,OPTIONS');
    // res.header('Content-Type', 'application/json;charset=utf-8');
		next();
});

var user_path = './data/database.json';
var doctor_path = './data/doctor-database.json';



// table - doctor
app.post('/api/doctor', function (req, res) {
	var dataList = [];
  var cur_data = {};
  var flag;
  console.log(req.body)
  cur_data = req.body;
  console.log((cur_data), typeof(cur_data));
  fs.readFile(doctor_path, function(err, data) {
    dataList = data && data.toString() ? JSON.parse(data.toString()) : [];
    (flag = dataList.find(function(v, i, list) {
      return v.id === cur_data.id
    })) ? dataList.forEach(function(v) {
      if(v.id === cur_data.id) {
        Object.assign(v, cur_data)
      }
    }) : dataList.push(cur_data);
    var result = JSON.stringify(dataList);
    console.log(result);
    fs.writeFile(doctor_path, result, function(err) {
      if(err) {
        console.log(err);
      } else {
        sendMsg(flag ? Object.assign(cur_data, {
          type: 'doctor-edit',
        }) : Object.assign(cur_data, {
          type: 'doctor-add'
        }));
        res.end(JSON.stringify({
          code: 20000,
          data: null,
          msg: '提交成功'
        }));
      }
    });
	})
});
app.get('/api/doctorList', function (req, res) {
	var dataList;

	fs.readFile(doctor_path, function(err, data) {
    if(err) {
      console.log(err);
    } else {
      console.log(dataList = data && data.toString() ? JSON.parse(data.toString()) : []);
      res.end(JSON.stringify({
        code: 20000,
        list: dataList,
        count: dataList.length,
        msg: '获取成功'
      }));
    }
	})
});

////////

// table - user
app.get('/api/userList', function (req, res) {
	var dataList;

	fs.readFile(user_path, function(err, data) {
    if(err) {
      console.log(err);
    } else {
      console.log(dataList = data && data.toString() ? JSON.parse(data.toString()) : []);
      res.end(JSON.stringify({
        code: 20000,
        list: dataList,
        count: dataList.length,
        msg: '获取成功'
      }));
    }
	})
});

app.post('/api/user', function (req, res) {
	var dataList = [];
  var cur_data = {};
  var flag;
  console.log(req.body)
  cur_data = req.body;
  console.log((cur_data), typeof(cur_data));
  fs.readFile(user_path, function(err, data) {
    dataList = data && data.toString() ? JSON.parse(data.toString()) : [];
    (flag = dataList.find(function(v, i, list) {
      return v.id === cur_data.id
    })) ? dataList.forEach(function(v) {
      if(v.id === cur_data.id) {
        Object.assign(v, cur_data)
      }
    }) : dataList.push(cur_data);
    var result = JSON.stringify(dataList);
    console.log(result);
    fs.writeFile(user_path, result, function(err) {
      if(err) {
        console.log(err);
      } else {
        sendMsg(flag ? Object.assign(cur_data, {
          type: 'user-edit',
        }) : Object.assign(cur_data, {
          type: 'user-add'
        }));
        res.end(JSON.stringify({
          code: 20000,
          data: null,
          msg: '提交成功'
        }));
      }
    });
	})
});

app.get('/api/user/info', function(req, res) {
  res.end(JSON.stringify({
    code: 20000,
    data: {
      avatar: "https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif",
      introduction: "I am a administrator",
      name: "Admin",
      roles: ["admin"],
    }
  }))
})

app.post('/api/user/login', function(req, res) {
  var { username, password } = req.body
  if(username == 'admin' && password === '111111') {
    res.end(JSON.stringify({
      code: 20000,
      data: {
        token: 'admin'
      }
    }))
  } else {
    res.end(JSON.stringify({
      code: 40000,
      msg: '账号或者密码错误'
    }))
  }
})

app.post('/api/user/logout', function(req, res) {
  res.end(JSON.stringify({
    code: 20000,
    data: 'success'
  }))
})

var server = app.listen(8090, function() {
	var host = server.address().address
  var port = server.address().port

  console.log("应用实例，访问地址为 http://%s:%s", host, port)
	// open('http://localhost:8090/dist/')
});


server.on('close', function() {
		console.log('development server stopped.');
});
// eslint-disabled
