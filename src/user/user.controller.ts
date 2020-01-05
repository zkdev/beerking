import {Body, Controller, Get, HttpException, HttpStatus, Param, Post} from '@nestjs/common';
import { UserService } from './user.service';
import { User } from "./user.entity";
import {UserDto} from "./user.dto";

@Controller('user')
export class UserController {

  constructor(private readonly userService: UserService) {}

  @Get(":username")
  async get(@Param() params): Promise<User[]> {
    return await this.userService.findByUsername(params.username);
  }

  @Get()
  async getAll(): Promise<User[]> {
    return await this.userService.findAll();
  }

  @Post()
  async register(@Body() userDto: UserDto): Promise<User> {
    return await this.userService.register(userDto);
  }
}
