import {IsEmail, Length} from "class-validator";

export class UserDto {
    @Length(3, 16)
    username: string;

    @Length(128, 128)
    passwd: string;

    @IsEmail()
    mail: string;
}
