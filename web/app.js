var app = angular.module('app', ['ngCookies']);

app.controller('MainCtrl', function($http, $cookies, $cookieStore) {
    var main = this;
    main.registerInfo = {};
    main.loginInfo = {};
    main.requests = [];
    main.friends = [];
    main.posts = [];
    main.circles = [];
    main.postCircle = null;
    main.postText = "";
    main.postImage = undefined;
    main.loggedIn = false;
    main.login = login;
    main.register = register;
    main.newCircle = newCircle;
    main.logout = logout;
    main.addFriend = addFriend;
    main.me = undefined;
    main.requestResponse = requestResponse;
    main.displayFriend = displayFriend;
    main.newPost = newPost;
    main.addToCircle = addToCircle;

    init();

    function init() {
        if ($cookies.session && $cookies.email) {
            main.loggedIn = true;
            main.me = $cookies.email;
            retrieveData();
        }
    }

    function login(email, password) {
        $http({
            url: '/login',
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            data: JSON.stringify({
                username: email,
                password: password
            })
        }).success(function() {
            $cookies.email = email;
            main.me = email;
            retrieveData();
            var session = Math.random().toString(36).replace(/[^a-z]+/g, '').substr(0, 10);
            $cookies.session = session;
            $('#registerModal').modal('hide');
            main.loggedIn = true;
        }).error(function() {
            alert("Failed Authentication");
        })
    }

    function retrieveData() {
        $http.get('/waitlist/' + $cookies.email)
            .success(function(data) {
                var list = data["waiting list"];
                main.requests = _.uniq(list);
            });

        $http.get('/friends/' + $cookies.email)
            .success(function(data) {
                main.friends = data.friends;
            });

        $http.get('/circle_amount/' + $cookies.email)
            .success(function(data){
                var circ_num = data.circles;
                for(var i = 1; i <= circ_num; i++) {
                    main.circles.push(i);
                }
            });

        $http({
            url: '/newsfeed',
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            data: JSON.stringify({
                username: $cookies.email
            })
        }).success(function(data) {
            main.posts = data.feed;
        })
    }

    function register(registerInfo) {
        if (registerInfo.password != registerInfo.repass) {
            alert("Passwords don't match");
        } else {
            //console.log(JSON.stringify(registerInfo));
            $http({
                url: '/register',
                method: "POST",
                headers: { 'Content-Type': 'application/json' },
                data: JSON.stringify({
                    username: registerInfo.email,
                    password: registerInfo.password
                })
            }).success(function() {
                $cookies.email = registerInfo.email;
                var session = Math.random().toString(36).replace(/[^a-z]+/g, '').substr(0, 10);
                $cookies.session = session;
                alert("Successed!");
                $('#registerModal').modal('hide');
                main.loggedIn = true;
            })
        }
    }

    function newCircle() {
        main.circles.push(main.circles.length + 1);
    }

    function logout() {
        $cookieStore.remove('email');
        $cookieStore.remove('session');

        main.registerInfo = {};
        main.loginInfo = {};
        main.requests = [];
        main.friends = [];
        main.posts = [];
        main.circles = [];
        main.loggedIn = false;
        main.me = undefined;
        main.postCircle = null;
        main.postText = "";
        main.postImage = undefined;
    }

    function addFriend(friend) {
        $http({
            url: '/add',
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            data: JSON.stringify({
                username: $cookies.email,
                target: friend
            })
        }).success(function() {
            alert('Request sent');
            main.friendEmail = '';
        }).error(function() {
            alert('Failed to send friend request');
            main.friendEmail = '';
        });
    }

    function requestResponse(accept, target) {
        var result = 'n';
        if (accept) {
            result = 'accept';
        }
        $http({
            url: '/response',
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            data: JSON.stringify({
                username: $cookies.email,
                target: target,
                result: result
            })
        }).success(function() {
            if (accept) {
                main.friends.push({
                    email: target,
                    circle: 0
                })
            }
            var i = main.requests.indexOf(target);
            if(i != -1) {
                main.requests.splice(i, 1);
            }

        });
    }

    function displayFriend(email, circle) {
        if (circle == 0) {
            return email
        } else {
            return email + " in Circle " + circle;
        }
    }

    function newPost(circle, text) {
        var image = document.getElementById('imageURI').value;
        $http({
            url: '/post',
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            data: JSON.stringify({
                username: $cookies.email,
                text: text,
                circle: circle,
                picture: image
            })
        }).success(function() {
            alert('Succeed');
            main.postCircle = null;
            main.postText = "";
            main.postImage = undefined;

            $http({
                url: '/newsfeed',
                method: "POST",
                headers: { 'Content-Type': 'application/json' },
                data: JSON.stringify({
                    username: $cookies.email
                })
            }).success(function(data) {
                main.posts = data.feed;
            })
        });
    }

    function addToCircle(friend, circle) {
        $http({
            url: '/add_circle/' + $cookies.email,
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            data: JSON.stringify({
                friend_name: friend.email,
                circle_num: circle
            })
        }).success(function() {
            friend.circle = circle;
        })
    }


});
