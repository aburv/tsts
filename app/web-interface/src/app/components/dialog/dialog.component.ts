import { Component, Input, TemplateRef } from '@angular/core';

@Component({
  selector: 'app-dialog',
  templateUrl: 'dialog.component.html',
  styleUrls: ['dialog.component.css'],
})
export class DialogComponent {
  @Input()
  content!: TemplateRef<any>;
}
