import { Component, OnInit, ElementRef, ViewChild } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';import {DdbbServices } from '../../services/ddbb.service';

@Component({
  selector: 'app-rag-ddbb',
  standalone: true,
  imports: [CommonModule,  RouterLink, FormsModule],
  templateUrl: './rag-ddbb.component.html',
  styleUrl: './rag-ddbb.component.scss'
})

export class RagDdbbComponent {

}
