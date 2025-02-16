from django.db import models

# Create your models here.

class ReferenceBook(models.Model):
    id = models.AutoField(
        primary_key=True,
        verbose_name='Идентификатор')
    code = models.CharField(
        max_length=100, 
        null=False, 
        verbose_name='код справочника', 
        unique=True)
    name = models.CharField(
        max_length=300, 
        null=False,
        verbose_name='название')
    description = models.TextField(blank=True, verbose_name='описание')
    
    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = 'Справочник'
        verbose_name_plural = 'Справочники'
    
    
class ReferenceBookVersion(models.Model):
    id = models.AutoField(
        primary_key=True, 
        verbose_name='Идентификатор')
    reference_book = models.ForeignKey(
        ReferenceBook,
        on_delete=models.CASCADE,
        related_name='versions',
        verbose_name='Идентификатор справочника',
        help_text='Справочник, к которому относится версия'
    )
    version = models.CharField(max_length=50)
    start_date = models.DateField(
        verbose_name='Дата начала действия версии',  
        help_text='Дата начала действия версии')

    def __str__(self):
        return f"{self.reference_book.code} - Версия {self.version} ({self.start_date})"

    class Meta:
        verbose_name = 'Версия справочника'
        verbose_name_plural = 'Версии справочников'
        constraints = [
            #Не может существовать более одной Версии с одинаковым набором значений "Идентификатор справочника" и "Версия".
            models.UniqueConstraint(
                fields=['reference_book', 'version'],
                name='unique_reference_book_version'
            ),
            # У одного Справочника не может быть более одной версии с одинаковой "Датой начала".
            models.UniqueConstraint(
                fields=['reference_book', 'start_date'],
                name='unique_reference_book_start_date'
            )
        ]
        
        
class ReferenceBookElement(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='Идентификатор')
    version = models.ForeignKey(
        ReferenceBookVersion,
        on_delete=models.CASCADE,
        related_name='elements',
        verbose_name='Идентификатор версии справочника',
        help_text='Версия справочника, к которой относится элемент'
    )
    code = models.CharField(
        max_length=100,
        verbose_name= 'Код элемента',
        help_text= 'Код элемента справочника (макс. 100 символов)'
    )
    value = models.CharField(
        max_length=300,
        verbose_name='Значение элемента',
        help_text='Значение элемента справочника (макс. 300 символов)'
    )

    def __str__(self):
        return f"{self.code} - {self.value}"

    class Meta:
        verbose_name = 'Элемент справочника'
        verbose_name_plural = 'Элементы справочников'
        constraints = [
            models.UniqueConstraint(
                # В одной Версии справочника не может существовать более одного Элемента справочника с одинаковым значением в поле Код.
                fields=['version', 'code'],
                name='unique_version_element_code'
            )
        ]