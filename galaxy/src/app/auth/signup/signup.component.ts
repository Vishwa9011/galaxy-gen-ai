import { Component } from '@angular/core';
import { NgForm } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent {
  username: string = '';
  password: string = '';
  role: string = '';

  constructor(private http: HttpClient) { }

  ngOnInit() { }

  async register() {
    console.log('username: ', this.username);
    console.log('password: ', this.password);
    console.log('role: ', this.role);

    if (!this.username || !this.password || !this.role) {
      return alert("fill all fields")
    }

    const body = {
      username: this.username,
      password: this.password,
      role: this.role
    };

    try {
      const apiUrl = `${environment.apiUrl}/signup`;
      const res = await this.http.post(apiUrl, body).toPromise();
      console.log('res: ', res);
    } catch (error) {
      console.error('Error:', error);
    }
  }
}
