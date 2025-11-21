import { Component, effect, input } from '@angular/core';
import { CommonModule } from '@angular/common';

import { ImageService } from 'src/app/_services/image.service';
import { ButtonComponent, ButtonType } from '../button/button.component';
import { Icon } from '../icon/icon.component';

@Component({
  selector: 'app-image',
    imports: [
    CommonModule,
    ButtonComponent,
  ],
  templateUrl: './image.component.html',
  styleUrl: './image.component.css'
})
export class ImageComponent {
  readonly ButtonType = ButtonType

  id = input.required<string>();
  icon = input.required<Icon>();
  size = input.required<number>();
  alt = input.required<string>();

  imageData: string | null = null;

  constructor(private image: ImageService) {
    effect(() => {
      const id = this.id();
      const size = this.size();

      if (id !== "") {
        this.fetch(id, size);
      }
    })
  }

  fetch(id: string, size: number): void {
    let imgRes = ""
    if (size < 80) {
      imgRes = "80"
    }
    this.image.get(id, imgRes).subscribe(data => {
      const blob = new Blob([data], { type: 'image/jpeg' });

      const reader = new FileReader();
      reader.onload = () => {
        this.imageData = reader.result as string;
      };
      reader.readAsDataURL(blob);
    });
  }
}
