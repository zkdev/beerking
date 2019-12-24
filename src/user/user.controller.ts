import { Body, Controller, Post } from '@nestjs/common';
import { UserService } from './user.service';
import { RegisterUserDto } from '../register-user-dto';
import {User} from "../entity/User";

@Controller('user')
export class UserController {

  constructor(private readonly userService: UserService) {}

  @Post()
  register(@Body() body: RegisterUserDto): User {
    // TODO return session
    return this.userService.register(body);
  }

}
