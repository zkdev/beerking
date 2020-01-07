import {IsEmail, Length} from "class-validator";

export class RegisterUserDto {
    @Length(3, 16)
    username: string;

    @Length(128)
    password: string;

    @IsEmail()
    mail: string;
}
