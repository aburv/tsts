import { ComponentRef, NO_ERRORS_SCHEMA } from '@angular/core';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';

import { ChipSetComponent } from './chip-set.component';

describe('ChipSetComponent', () => {
  let componentRef: ComponentRef<ChipSetComponent>;
  let fixture: ComponentFixture<ChipSetComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ChipSetComponent],
      schemas: [NO_ERRORS_SCHEMA],
    })
      .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ChipSetComponent);
    componentRef = fixture.componentRef;
  });

  it('Should create', () => {
    expect(componentRef).toBeTruthy();
  });

  it('View: Should have parent tag with content css class', () => {
    const content = fixture.nativeElement.querySelector('.content');

    expect(content).not.toBe(null);
  });

  it('View: Should list the options text with item css class', () => {
    const options = [{ id: "optionId1", text: 'optionText1' }, { id: "optionId2", text: 'optionText2' }];
    const selected = ["optionId1"];

    spyOn(fixture.componentInstance.childEmitter, 'emit');
    componentRef.setInput("options", options);
    componentRef.setInput("selected", selected);

    fixture.detectChanges();

    const items = fixture.debugElement.queryAll(By.css('.item'));
    for (let i = 0; i < items.length; i++) {
      const itemElement = items[i].nativeElement;
      expect(itemElement.textContent.trim()).toBe(options[i].text);
      if(selected.includes(options[i].id)){
        expect(items[i].classes['selected']).toBe(true); 
      }
    }

    items[0].nativeElement.click();
    
    expect(fixture.componentInstance.childEmitter.emit).toHaveBeenCalledWith('optionId1');
  });

});
