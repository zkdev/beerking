import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { User } from './user.entity';
import {RegisterUserDto} from "./dto/register-user.dto";

@Injectable()
export class UserService {
    constructor(@InjectRepository(User) private readonly userRepository: Repository<User>) {}

    findAll(): Promise<User[]> {
        return this.userRepository.find();
    }

    findByUsername(username: string): Promise<User[]> {
        return this.userRepository.find({where: {"username": username}});
    }

    register(userDto: RegisterUserDto): Promise<User> {
        const uuidv4 = require('uuid/v4');
        const user = new User();
        user.mail = userDto.mail;
        user.passwd = userDto.password;
        user.username = userDto.username;
        //TODO make sure uuid is unique
        user.uuid = uuidv4();
        //TODO remove admin permissions for each new user
        user.roles = ['user', 'admin'];
        return this.userRepository.manager.save(user);
    }

    async delete(username: string) {
        const user = await this.userRepository.find({where: {"username": username}});
        await this.userRepository.manager.remove(user);
        return;
    }
}
