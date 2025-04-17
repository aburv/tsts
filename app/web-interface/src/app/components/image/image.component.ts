import { Component, effect, input } from '@angular/core';
import { ImageService } from 'src/app/_services/image.service';

@Component({
  selector: 'app-image',
  templateUrl: './image.component.html',
  styleUrl: './image.component.css'
})
export class ImageComponent {

  id = input.required<string>();
  icon = input.required<string>();
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
      // Convert binary data to a blob
      const blob = new Blob([data], { type: 'image/jpeg' });

      // Use FileReader to read the blob as a Data URL
      const reader = new FileReader();
      reader.onload = () => {
        // Update the imageUrl signal with the base64 data URL
        this.imageData = reader.result as string;
      };
      reader.readAsDataURL(blob);
    });
  }
}
