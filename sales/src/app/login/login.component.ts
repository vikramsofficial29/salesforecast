import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

interface LoginResponse {
  error : string;
  message : string;
}

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  username !: string;
  password !: string;
  errorMessage!: string;
  message!: string;

  constructor(private http: HttpClient, private router: Router) { }

  login() {
    if (!this.username || !this.password) {
      this.errorMessage = 'Fill in the required fields';
      return;
    }

    this.http.post<LoginResponse>('http://127.0.0.1:5000/login', { username: this.username, password: this.password })
      .subscribe(
        response => {
          if (response.error) {
            this.errorMessage = response.error;
            this.message = '';
          } else {
            this.message = response.message;
            if (this.message === 'Login successful') {
              // Redirect to the next page
              this.router.navigate(['/upload']);
            }
          }
        },
        error => {
          this.errorMessage = error.error;
          this.message = '';
        }
      );
  }
}

