import {Controller, Get, Post, Request, UseGuards} from '@nestjs/common';
import {AuthGuard} from "@nestjs/passport";
import {AuthService} from "./auth/auth.service";
import {Roles} from "./common/decorators/roles.decorator";
import {RolesGuard} from "./common/guards/roles.guard";

@Controller()
export class AppController {
  constructor(private readonly authService: AuthService) {}

  @UseGuards(AuthGuard('local'))
  @Post('login')
  async login(@Request() req) {
    return this.authService.login(req.user);
  }

  @UseGuards(AuthGuard('jwt'), RolesGuard)
  @Roles('admin')
  @Get('admin')
  async admin() {
    return "I am admin."
  }

  @UseGuards(AuthGuard('jwt'))
  @Get('profile')
  getProfile(@Request() req) {
    return req.user;
  }

}
