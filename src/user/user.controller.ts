import {Body, Controller, Delete, Get, Param, Post, Request, UseGuards} from '@nestjs/common';
import { UserService } from './user.service';
import { User } from "./user.entity";
import {RegisterUserDto} from "./dto/register-user.dto";
import {AuthGuard} from "@nestjs/passport";
import {RolesGuard} from "../common/guards/roles.guard";
import {Roles} from "../common/decorators/roles.decorator";

@Controller('user')
export class UserController {

  constructor(private readonly userService: UserService) {}

  @UseGuards(AuthGuard('jwt'))
  @Roles('admin')
  @Get(":username")
  async get(@Param() params): Promise<User[]> {
    return await this.userService.findByUsername(params.username);
  }

  @UseGuards(AuthGuard('jwt'), RolesGuard)
  @Roles('admin')
  @Get()
  async getAll(): Promise<User[]> {
    return await this.userService.findAll();
  }

  @Post()
  async register(@Body() userDto: RegisterUserDto): Promise<User> {
    return await this.userService.register(userDto);
  }

  @UseGuards(AuthGuard('jwt'), RolesGuard)
  @Roles('admin')
  @Delete(':username')
  async delete(@Param() params) {
    return await this.userService.delete(params.username)
  }

}
