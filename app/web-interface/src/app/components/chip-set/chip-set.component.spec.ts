import { NO_ERRORS_SCHEMA } from '@angular/core';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';

import { ChipSetComponent } from './chip-set.component';

describe('ChipSetComponent', () => {
  let component: ChipSetComponent;
  let fixture: ComponentFixture<ChipSetComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ChipSetComponent],
      schemas: [NO_ERRORS_SCHEMA],
    })
      .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ChipSetComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('Should create', () => {
    expect(component).toBeTruthy();
  });

  it('View: Should have parent tag with content css class', () => {
    const content = fixture.nativeElement.querySelector('.content');

    expect(content).not.toBe(null);
  });

  it('View: Should list the options text with item css class', () => {
    const options = [{ id: "optionId1", text: 'optionText1' }, { id: "optionId2", text: 'optionText2' }];
    const selected = ["optionId1"];

    spyOn(component.childEmitter, 'emit');
    component.options = options;
    component.selected = selected;
    fixture.detectChanges();

    const items = fixture.debugElement.queryAll(By.css('.item'));
    for (let i = 0; i < items.length; i++) {
      const itemElement = items[i].nativeElement;
      expect(itemElement.textContent).toBe(options[i].text);
      if(selected.includes(options[i].id)){
        expect(items[i].classes['selected']).toBe(true); 
      }
    }

    items[0].nativeElement.click();
    
    expect(component.childEmitter.emit).toHaveBeenCalledWith('optionId1');
  });

});
