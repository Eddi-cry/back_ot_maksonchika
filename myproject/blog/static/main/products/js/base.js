document.addEventListener('DOMContentLoaded', function() {
    const map = new jsVectorMap({
        selector: '#world-map',
        map: 'world',
        
        containerStyle: {
            width: '100%',
            height: '100%',
            position: 'absolute',
            top: 0,
            left: 0
        },

        markers: [
            { name: 'LOVJ', coords: [68.004660, 35.014156] },
            { name: 'Obninsk', coords: [57.117251, 39.596727] },
            { name: 'NRIL', coords: [69.343985, 88.210393] }
        ],
        
        lineStyle: {
            strokeWidth: 2,
            animation: true,
            strokeLinecap: 'round',
            fill: 'none'
        },
        
        lines: [
            {
                from: 'LOVJ',
                to: 'Obninsk',
                style: {
                    stroke: "#676767",
                    strokeDasharray: '6 3 6',
                    curvature: -0.9,
                    arc: 2,
                    animationDuration: 2000
                }
            },
            {
                from: 'NRIL',
                to: 'Obninsk',
                style: {
                    stroke: "#00aa00",
                    strokeDasharray: '8 2',
                    curvature: 0.9,
                    arc: 1.5,
                    animationDelay: 500
                }
            }
        ],

        zoom: {
            animation: {
            duration: 10000, // Продолжительность в миллисекундах (3 секунды)
            ease: 'easeOutQuad' // Тип сглаживания анимации
        }
    },
        
        focusOn: {
            regions: ['RU'],
            scale: 1.5, // Уменьшенный масштаб для фона
            animate: {
                duration: 4000,
                ease: 'easeInOutCubic'
            }
            
        },
        
        markerStyle: {
            initial: {
                fill: '#727cf5',
                stroke: '#fff',
                strokeWidth: 2,
                r: 5, // Уменьшенный размер для фона
            },
            hover: {
                fill: '#ff0000',
                r: 7
            }
        },
        
        regionStyle: {
            initial: {
                fill: '#e3eaef',
                stroke: '#a7b4c1',
                strokeWidth: 0.3 // Уменьшенная толщина границ
            },
            hover: {
                fill: '#d1d8e0'
            }
        },
        
        zoomOnScroll: false,
        zoomButtons: false, // Скрыты для фона
        backgroundColor: 'transparent'
    });

    // Обновление при изменении размера окна
    window.addEventListener('resize', function() {
        map.updateSize();
    });
});

document.getElementById('generateLinkBtn').addEventListener('click', function() {
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;
    
    if (!startDate || !endDate) {
        alert('Пожалуйста, выберите обе даты');
        return;
    }
    
    // Получаем CSRF токен
    const csrfToken = document.getElementById('csrf_token').value;
    // Или альтернативный способ:
    // const csrfToken = getCookie('csrftoken');
    
    fetch('/generate_download_link/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken  // Добавляем CSRF токен в заголовки
        },
        body: JSON.stringify({
            start_date: startDate,
            end_date: endDate
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.download_url) {
            const link = document.createElement('a');
            link.href = data.download_url;
            link.download = 'files_archive.zip';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        } else {
            alert(data.error || 'Произошла ошибка');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Произошла ошибка при формировании ссылки');
    });
});