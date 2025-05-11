//package com.hnu.muwu.controller;
//
//
//import com.hnu.muwu.bean.UserInfo;
//import com.hnu.muwu.service.UserService;
//import jakarta.annotation.Resource;
//
//import org.springframework.web.bind.annotation.CrossOrigin;
//import org.springframework.web.bind.annotation.RequestMapping;
//import org.springframework.web.bind.annotation.RequestMethod;
//import org.springframework.web.bind.annotation.RestController;
//
//import java.util.List;
//
//@CrossOrigin(origins = "*")
//@RestController
//@RequestMapping("/getAllUserInfo" )
//public class GetAllUserInfo {
//
//    @Resource
//    private UserService userService;
//
////    @RequestMapping(value = "/getAllUserInfo", method = RequestMethod.GET, produces = "application/json;charset=UTF-8")
////    public List<UserInfo> getAllUserInfo() {
////        System.out.println("getAllUserInfo");
////        List<UserInfo> users = userService.getAllUsers();
////        users.forEach(System.out::println);
////        for (UserInfo user : users) {
//////            System.out.println(user.getUserId());
////            System.out.println(user.getEmail());
////            System.out.println(user.getTelephone());
////        }
////        return users;
////    }
////}
//
//
//package com.hnu.muwu.controller;
//
//import com.hnu.muwu.bean.UserInfo;
//import com.hnu.muwu.service.UserService;
//import jakarta.annotation.Resource;
//import org.springframework.web.bind.annotation.*;
//
//        import java.util.List;
//
//@CrossOrigin(origins = "*")
//@RestController
//@RequestMapping("/users")  // 使用资源名词复数作为根路径
//public class UserController {
//
//    @Resource
//    private UserService userService;
//
//    // 使用 GET 方法获取资源集合，路径直接映射到根路径
//    @GetMapping  // 简化写法，等价于 @RequestMapping(method = RequestMethod.GET)
//    public List<UserInfo> getAllUsers() {
//        return userService.getAllUsers();
//    }
//}