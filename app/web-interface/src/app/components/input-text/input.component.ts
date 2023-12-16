import { Component, EventEmitter, Input, OnInit, Output, HostListener, ElementRef } from '@angular/core';

@Component({
  selector: 'app-input',
  templateUrl: './input.component.html',
  styleUrls: ['./input.component.css'],
})
export class InputComponent implements OnInit {
  @Input()
  public placeholder!: string;
  @Input()
  public title!: string;
  @Input()
  public value!: string;
  @Input()
  public type!: string;
  @Input()
  public validator!: string;
  @Output() public childEmitter = new EventEmitter();

  isFocus = false;
  isValid!: boolean;
  regex!: RegExp;

  @HostListener('document:click', ['$event'])
  clickout(event: any): void {
    if (!this.eRef.nativeElement.contains(event.target)) {
      this.isFocus = false;
    }
  }

  constructor(private eRef: ElementRef) { }

  regexes: any = {
    phone: /^([0-9]{10})$/,
    email: /^(([^<>()\\.,;:\s@"]+(\.[^<>()\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/,
    zip: /^[1-9][0-9]{5}$/,
    mandatory: /.+/,
    tableSeats: /^[0-9]{1}[0-9]{0,1}$/,
    currency: /^([A-Z]{3})$/,
    number: /^(?!(?:0|0\.0|0\.00)$)[+]?\d+(\.\d|\.\d[0-9])?$/,
    ip: /^([1-5]{1,3}).([1-5]{1,3}).([1-5]{1,3}).([1-5]{1,3})$/,
  };

  ngOnInit(): void {
    if (this.validator) {
      this.regex = new RegExp(this.regexes[this.validator]);
      this.title = this.title + '  *';
    }
  
    this.value = '';
  }

  onInput(event: any): void {
    const value = event.target.value;
    this.isValid = this.validator ? this.regex.test(value) : true;
    if (this.isValid) {
      this.childEmitter.emit(value);
    }
  }

  getBorderColor(): string {
    if (this.isValid !== undefined && this.isValid === false) { return 'var(--danger)'; }
    return this.isFocus ? 'var(--primary)' : 'var(--less-bright)';
  }
}
