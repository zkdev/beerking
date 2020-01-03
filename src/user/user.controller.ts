import {Body, Controller, Get, Param, Post} from '@nestjs/common';
import { UserService } from './user.service';
import { User } from "./user.entity";

@Controller('user')
export class UserController {

  constructor(private readonly userService: UserService) {}

  @Get(":username")
  async get(@Param() params): Promise<User[]> {
    return await this.userService.find(params.username);
  }

  @Get()
  async getAll(): Promise<User[]> {
    return await this.userService.findAll();
  }
}
