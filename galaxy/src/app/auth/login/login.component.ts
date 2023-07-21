import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  username = ''
  password = ''
  constructor(private http: HttpClient) { }

  ngOnInit() { }

  async login() {
    if (!this.username || !this.password) {
      return alert("fill all fields")
    }

    const body = {
      username: this.username,
      password: this.password,
    }

    try {
      const apiUrl = `${environment.apiUrl}/login`;
      const res = await this.http.post(apiUrl, body).toPromise()
      console.log('res: ', res);
    } catch (error) {
      console.log('error: ', error);
    }

  }
}
