import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-button',
  templateUrl: './button.component.html',
  styleUrls: ['./button.component.css']
})
export class ButtonComponent {

  @Input()
  public type!: string;
  @Input()
  public text!: string;
  @Input()
  public icon!: string;
  @Input()
  public iconColor!: string;
  @Input()
  public iconSize!: number;

}
