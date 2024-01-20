

import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

interface SignupResponse {
  error: string;
  message: string;
}

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})

export class SignupComponent {
  errorMessage !: string;
  username !: string;
  password !: string;
  email !: string;
  message !: string;
  showMessageFlag !: boolean;

  constructor(private http: HttpClient,private router: Router ) { }

  showMessage() {
    // Set the message content
    this.message = "Signup successful!";
    // Set the flag to true to show the message
    this.showMessageFlag = true;
  }

  signup() {
    const data = {
      username: this.username,
      password: this.password,
      email: this.email
    };

    console.log(this.username);


    this.http.post<SignupResponse>('http://127.0.0.1:5000/signup', data).subscribe(
      response => {
        if (response.error) {
          this.errorMessage = response.error;
          this.message = '';
        } else {
          this.errorMessage = '';
          // this.message = response.message;
          if (this.message === 'Signup successful!') {
            // Redirect to the next page
            this.router.navigate(['/login']);
          }
          const message = response.message;
          // Do something with the success message
          console.log(message);
        }
      },
      error => {
        this.errorMessage = 'Fill All the Boxes';
        this.message = '';
        console.error(error);
      }
    );
  }
}

