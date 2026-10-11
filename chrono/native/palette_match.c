int _fltused = 0;
void *memset(void *, int, unsigned long long);
#ifdef _MSC_VER
#pragma function(memset)
#endif
void *memset(void *dst, int value, unsigned long long count) { volatile unsigned char *p=(volatile unsigned char *)dst; while(count--)*p++=(unsigned char)value; return dst; }
typedef int int32_t;
typedef unsigned char uint8_t;
#define FLT_MAX 3.402823466e+38F
static float fmaxf(float a,float b){return a>b?a:b;}
#ifdef _WIN32
#define API __declspec(dllexport)
#else
#define API
#endif
/* Palette-only matching. No pixel buffers, rendering or cartridge bytes. */
API void match_block(const int32_t *ids, int n, const uint8_t *rgb, int pool,
                     const float *table, const float *q, const float *weights,
                     const float *bounds, const float *cost, int tone, int keep, float cutoff,
                     float *scores, int32_t *indices) {
    float worst=cutoff; int worst_at=0;
    const float channel[3]={.2126f,.7152f,.0722f};
    float mean[3]={0,0,0},second[3]={0,0,0};
    for(int k=0;k<8;k++)for(int c=0;c<3;c++){
        float v=q[k*3+c]/255;mean[c]+=weights[k]*v;second[c]+=weights[k]*v*v;
    }
    for(int k=0;k<keep;k++){scores[k]=cutoff;indices[k]=-1;}
    for(int i=0;i<n;i++) {
        const int32_t *pal=ids+i*8; float score=0, normalized[8][3];
        float gains[3],offsets[3],exposure=1e-6f;
        if(tone) {
            for(int c=0;c<3;c++) {
                float lo=255,hi=0;
                for(int j=0;j<8;j++){float v=rgb[pal[j]*3+c];if(v<lo)lo=v;if(v>hi)hi=v;}
                float black=bounds[c], white=bounds[3+c];
                if(white-black<8){black=0;white=255;}
                float gain=(hi-lo)/fmaxf(white-black,1);if(gain>3)gain=3;
                float off=lo-black*gain;
                gains[c]=gain;offsets[c]=off;if(gain>exposure)exposure=gain;
                for(int j=0;j<8;j++)normalized[j][c]=(rgb[pal[j]*3+c]-off)/fmaxf(gain,1e-6f)/255;
                float qlo=255,qhi=0;
                for(int k=0;k<8;k++)if(weights[k]>0){float v=q[k*3+c];if(v<qlo)qlo=v;if(v>qhi)qhi=v;}
                if(gain<1e-6f && qhi-qlo>8)score+=.25f/3;
            }
        }
        if(tone) {
            /* One common exposure shift is free; RGB casts/black-point loss are not. */
            for(int c=0;c<3;c++) {
                float slope=gains[c]/exposure-1,shift=offsets[c]/exposure/255;
                score+=channel[c]*(slope*slope*second[c]+2*slope*shift*mean[c]+shift*shift);
            }
        }
        for(int k=0;k<8 && score<=worst;k++) {
            if(weights[k]<=0)continue;
            float best=FLT_MAX; int selected=0;
            for(int j=0;j<8;j++) {
                float d;
                if(tone){float r=normalized[j][0]-q[k*3]/255,g=normalized[j][1]-q[k*3+1]/255,b=normalized[j][2]-q[k*3+2]/255;d=.2126f*r*r+.7152f*g*g+.0722f*b*b;}
                else d=table[k*pool+pal[j]];
                if(d<best){best=d;selected=j;}
            }
            score+=weights[k]*(best+cost[i*8+selected]);
        }
        if(score<worst) {
            scores[worst_at]=score;indices[worst_at]=i;
            worst_at=0;for(int k=1;k<keep;k++)if(scores[k]>scores[worst_at])worst_at=k;
            worst=scores[worst_at];
        }
    }
}
